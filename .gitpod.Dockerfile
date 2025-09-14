# Gitpod'un standart workspace imajını temel alıyoruz.
FROM gitpod/workspace-full

# Root kullanıcıya geçiyoruz ki Docker kurabilelim.
USER root

# Docker'ın en son versiyonunu kuruyoruz.
RUN curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# Gitpod kullanıcısını docker grubuna ekliyoruz ki sudo gerekmesin.
RUN usermod -aG docker gitpod

# Tekrar varsayılan gitpod kullanıcısına dönüyoruz.
USER gitpod